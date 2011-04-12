====================================================
**reStructuredText**
====================================================

For details, see `Wiki`_.
.. _`Wiki`: http://www.wikipedia.org/

.. image:: like.jpg
    :scale: 70 %
    :align: center

Feature
--------------

* 支援中文::

    哈囉，reStructuredText！
    
* Easy to 
    * **read**
    * *write*

* Easy to format::

    native int  rsnScriptCCreate(int con, String val);
    synchronized int /*Better name: NScriptCCreate*/ nScriptCCreate(String val) 
    {  // Terrible naming. This "nScriptCCreate" is different from 
       // the (void*)nScriptCCreate above. This "nScriptCCreate" is invoked by 
       // ScriptC.java
        return rsnScriptCCreate(mContext, val);
    }

* *Nice Converter*::

    1. http://docutils.sourceforge.net/
    2. http://rst2a.com/create/type/

Table Demo
------------------------------------------------------

.. list-table:: API prefix table
    :header-rows: 1

    * - Component
      - Prefix
      - Comments
    * - libRS.so
      - 
      - File names are prefixed with rs\*
    * - 
      - rsi_*() in rsScriptC.cpp (e.g., esi_ScriptCreate(), which will call 
        ScriptCState::runCompiler())
      - RS API real implementation (The rs*() finally routes here)
    * - 
      - SC_X() in rsScriptC_lib.cpp (e.g., X = drawsimplemesh)
      - Rendering API provided by RenderScript for BCC (In BCC, you cal call 
        this API by X(...)) Most of the APIs are implemented in OpenGL (ES)
    * - RS Command
      - rs\*()
      - the commands, rsgApi.cpp
    * - 
      - RS_CMD_*
      - parameter data structure for the command
    * - 
      - RS_CMD_ID_*
      - command ID (an integer constant)
    * - 
      - rsp_*()
      - playback function (rs*()->...->rsp_*()->rsi_*()), rsgApiReplay.cpp
    * - JNI
      - n\*() in android_renderscript_renderscript.cpp
      - *n* stands for *native*

