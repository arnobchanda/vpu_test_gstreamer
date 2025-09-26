import sys
import gi

# Require GStreamer 1.0
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib

# --- Main Function ---
def main():
    # 1. Initialize GStreamer
    # It's important to do this before using any other GStreamer elements.
    Gst.init(sys.argv)

    # 2. Define the GStreamer pipeline
    # This is the same syntax as gst-launch-1.0
    # rtspsrc: Connects to the RTSP stream.
    # decodebin: Automatically finds the correct parsers and decoders.
    # autovideosink: Automatically finds the best video output for your system.
    rtsp_url = "rtsp://admin:root%40ReVx@192.168.50.109/Streaming/Channels/101"
    
    # You can replace the rtsp_url with your own camera's URL
    # For example: "rtsp://admin:password@192.168.1.100/stream1"
    
    pipeline_str = f"rtspsrc location={rtsp_url} latency=200 ! decodebin ! autovideoconvert ! queue ! waylandsink qos=false sync=false"

    print(f"Creating pipeline: {pipeline_str}")
    pipeline = Gst.parse_launch(pipeline_str)

    # 3. Start the pipeline
    pipeline.set_state(Gst.State.PLAYING)

    # 4. Wait for the pipeline to finish or for a keyboard interrupt (Ctrl+C)
    print("Pipeline is running. Press Ctrl+C to stop.")
    try:
        loop = GLib.MainLoop()
        loop.run()
    except KeyboardInterrupt:
        print("Stopping pipeline.")
        pipeline.set_state(Gst.State.NULL)
        loop.quit()

if __name__ == "__main__":
    sys.exit(main())