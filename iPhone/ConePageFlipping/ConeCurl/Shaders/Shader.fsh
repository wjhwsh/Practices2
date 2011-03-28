//
//  Shader.fsh
//  ConeCurl
//
//  Created by W. Dana Nuon on 4/18/10.
//  Copyright W. Dana Nuon 2010. All rights reserved.
//

varying lowp vec4 colorVarying;

void main()
{
    gl_FragColor = colorVarying;
}
