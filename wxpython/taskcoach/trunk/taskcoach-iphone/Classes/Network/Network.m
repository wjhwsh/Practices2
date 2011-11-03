//
//  Network.m
//  TaskCoach
//
//  Created by Jérôme Laheurte on 17/01/09.
//  Copyright 2009 Jérôme Laheurte. See COPYING for details.
//

#include <netinet/in.h>
#include <netinet/tcp.h>
#include <sys/socket.h>

#import "Network.h"

@interface Buffer : NSObject
{
	NSData *data;
	NSInteger offset;
}

@property (nonatomic, retain) NSData *data;
@property (nonatomic) NSInteger offset;

- initWithData:(NSData *)data;

@end

@implementation Network

- initWithAddress:(NSString *)address port:(NSInteger)port delegate:(id <NetworkDelegate>)theDelegate
{
	if ((self = [super init]))
	{
		delegate = theDelegate;
		
		CFReadStreamRef iStream;
		CFWriteStreamRef oStream;
		CFStreamCreatePairWithSocketToHost(NULL, (CFStringRef)address, port, &iStream, &oStream);
		
		if (!iStream || !oStream)
		{
			[self dealloc];
			return nil;
		}
		
		inputStream = (NSInputStream *)iStream;
		outputStream = (NSOutputStream *)oStream;
		
		[inputStream setDelegate:self];
		[outputStream setDelegate:self];
		
		[inputStream scheduleInRunLoop:[NSRunLoop currentRunLoop] forMode:NSDefaultRunLoopMode];
		[outputStream scheduleInRunLoop:[NSRunLoop currentRunLoop] forMode:NSDefaultRunLoopMode];

		[inputStream open];
		[outputStream open];
		
		data = [[NSMutableData data] retain];
		toSend = [[NSMutableArray alloc] init];
		
		expecting = -1;
	}
	
	return self;
}

- (void)dealloc
{
	[inputStream close];
	[inputStream removeFromRunLoop:[NSRunLoop currentRunLoop] forMode:NSDefaultRunLoopMode];
	[outputStream close];
	[outputStream removeFromRunLoop:[NSRunLoop currentRunLoop] forMode:NSDefaultRunLoopMode];

	[inputStream release];
	[outputStream release];
	[data release];
	[toSend release];
	
	[super dealloc];
}

- (void)pumpData
{
	if (expecting > 0)
	{
		NSInteger offset = 0;
		
		if ([data length] - offset >= expecting)
		{
			NSData *recvd = [NSData dataWithBytes:[data bytes] + offset length:expecting];
			offset += expecting;
			
			NSMutableData *newData = [[NSMutableData alloc] initWithBytes:[data bytes] + offset length:[data length] - offset];
			[data release];
			data = newData;
			expecting = -1;

			[delegate network:self didGetData:recvd];
		}
	}
	else if (expecting == 0)
	{
		[delegate network:self didGetData:[NSData dataWithBytes:NULL length:0]];
	}
}

- (void)expect:(NSInteger)bytes
{
	expecting = bytes;
	[self pumpData];
}

- (void)writeToStream:(NSStream *)stream
{
	Buffer *bf = [toSend objectAtIndex:0];
	unsigned int len = 0;
	
	len = [(NSOutputStream *)stream write:(uint8_t *)[bf.data bytes] + bf.offset maxLength:[bf.data length] - bf.offset];
	bf.offset += len;
	if (bf.offset == [bf.data length])
	{
		[toSend removeObjectAtIndex:0];
	}
}	

- (void)append:(NSData *)theData
{
	Buffer *bf = [[Buffer alloc] initWithData:theData];
	[toSend addObject:bf];
	[bf release];
	
	if (!writing && [outputStream hasSpaceAvailable])
		[self writeToStream:outputStream];
}

- (void)appendInteger:(int32_t)value
{
	value = htonl(value);
	[self append:[NSData dataWithBytes:&value length:sizeof(value)]];
}

- (void)appendString:(NSString *)string
{
	if (string)
	{
		const char *bf = [string UTF8String];
		int32_t len = strlen(bf);

		[self appendInteger:len];
		
		if (len)
			[self append:[NSData dataWithBytes:bf length:len]];
	}
	else
	{
		[self appendInteger:0];
	}
}

- (void)close
{
	[inputStream close];
	[outputStream close];
}

- (void)stream:(NSStream *)stream handleEvent:(NSStreamEvent)eventCode
{
	switch (eventCode)
	{
		case NSStreamEventOpenCompleted:
			connectionCount += 1;
			if (connectionCount == 2)
			{
				[delegate networkDidConnect:self];

				CFDataRef sock = CFWriteStreamCopyProperty((CFWriteStreamRef)outputStream, kCFStreamPropertySocketNativeHandle);
				if (sock)
				{
					CFSocketNativeHandle fd;
					CFDataGetBytes(sock, CFRangeMake(0, CFDataGetLength(sock)), (UInt8 *)&fd);
					int v = 1;
					setsockopt(fd, IPPROTO_TCP, TCP_NODELAY, &v, sizeof(v));
					CFRelease(sock);
				}
			}
			break;
		case NSStreamEventEndEncountered:
			[delegate networkDidClose:self];
			break;
		case NSStreamEventErrorOccurred:
			[delegate networkDidEncounterError:self error:[stream streamError]];
			break;
		case NSStreamEventHasBytesAvailable:
		{
			uint8_t buffer[1024];
			NSInteger len = 0;

			len = [(NSInputStream *)stream read:buffer maxLength:1024];
			
			if (len >= 0)
			{
				[data appendBytes:buffer length:len];
				[self pumpData];
			}

			break;
		}
		case NSStreamEventHasSpaceAvailable:
		{
			if ([toSend count])
			{
				writing = YES;
				[self writeToStream:stream];
			}
			else
			{
				writing = NO;
			}

			break;
		}
	}
}

@end

@implementation Buffer

@synthesize data;
@synthesize offset;

- initWithData:(NSData *)theData
{
	if ((self = [super init]))
	{
		data = [theData retain];
	}
	
	return self;
}

- (void)dealloc
{
	[data release];
	
	[super dealloc];
}

@end
