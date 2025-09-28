import sys
import gi
gi.require_version("Gst", "1.0")
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

    # The decodebin is using the /dev/imx_hantro device.
    # We need to use imxvideoconvert_g2d device for VPU 2D convert
    # pipeline_str = f"rtspsrc location={rtsp_url} latency=0 ! decodebin ! videoconvert ! v4l2sink device=/dev/video10" #<- This is working.
    pipeline_str = f"rtspsrc location={rtsp_url} latency=100 do-retransmission=false ! decodebin ! queue max-size-buffers=2 leaky=downstream ! videoconvert ! v4l2sink device=/dev/video10 sync=false"
    # pipeline_str = (
    # f"rtspsrc location={rtsp_url} latency=100 do-retransmission=false ! "
    # "queue max-size-buffers=2 leaky=downstream ! "
    # "rtph264depay ! h264parse config-interval=-1 ! "
    # "video/x-h264,stream-format=byte-stream,alignment=au ! "
    # "vpudec ! videoconvert ! "
    # "video/x-raw,format=RGB,width=1280,height=720,framerate=25/1 ! "
    # "v4l2sink device=/dev/video10 sync=false"
    # )




    # pipeline_str = f"rtspsrc location={rtsp_url} latency=200 ! queue max-size-buffers=2 leaky=downstream ! rtph264depay ! h264parse ! vpudec ! queue max-size-buffers=2 ! videoconvert ! video/x-raw,format=YUY2 ! v4l2sink device=/dev/video10 sync=false"
    # pipeline_str = f"rtspsrc location={rtsp_url} latency=200 ! queue max-size-buffers=2 leaky=downstream ! rtph264depay ! h264parse ! vpudec ! queue max-size-buffers=2 ! v4l2sink device=/dev/video10 sync=false"
    # pipeline_str = f"videotestsrc ! video/x-raw,format=YUY2,width=640,height=480 ! v4l2sink device=/dev/video10"
    # pipeline_str = f"rtspsrc location={rtsp_url} latency=200 ! queue max-size-buffers=2 leaky=downstream ! rtph264depay ! h264parse ! vpudec ! videoconvert ! video/x-raw,format=YUY2,width=640,height=480 ! v4l2sink device=/dev/video10 sync=false"
    
    # THis works but gives greenscreen
    # pipeline_str = f"rtspsrc location={rtsp_url} latency=200 ! queue max-size-buffers=2 leaky=downstream ! rtph264depay ! h264parse ! vpudec ! videoconvert ! video/x-raw,format=YUY2,width=1280,height=720 ! v4l2sink device=/dev/video10 sync=false"

    # pipeline_str = f"rtspsrc location={rtsp_url} latency=200 ! queue max-size-buffers=2 leaky=downstream ! rtph264depay ! h264parse ! vpudec ! videoconvert ! video/x-raw,format=RGB,width=1280,height=720 ! v4l2sink device=/dev/video10 sync=false"
    # pipeline_str = f"rtspsrc location={rtsp_url} latency=200 ! queue max-size-buffers=2 leaky=downstream ! rtph264depay ! h264parse ! vpudec ! videoconvert ! v4l2sink device=/dev/video10 sync=false"
    # pipeline_str = f"rtspsrc location={rtsp_url} latency=200 ! queue max-size-buffers=2 leaky=downstream ! rtph264depay ! h264parse ! vpudec  ! videoconvert ! capsfilter name=filter ! v4l2sink device=/dev/video10 sync=false"
    # pipeline_str = f"rtspsrc location={rtsp_url} latency=0 ! queue max-size-buffers=2 leaky=downstream ! rtph264depay ! h264parse config-interval=-1 ! capsfilter name=filter ! vpudec  ! videoconvert ! video/x-raw,format=I420,width=1280,height=720 ! v4l2sink device=/dev/video10 sync=false"

    # pipeline_str = f"rtspsrc location={rtsp_url} latency=0 ! rtph264depay ! h264parse ! vpudec ! vpuenc_h264 ! h264parse ! v4l2sink device=/dev/video10 sync=false"
    # pipeline_str = f"rtspsrc location={rtsp_url} latency=0 ! rtph264depay ! h264parse ! vpudec ! vpuenc_h264 ! v4l2sink device=/dev/video10 sync=false"
    
    # pipeline_str = f"rtspsrc location={rtsp_url} latency=0 ! rtph264depay ! h264parse ! vpudec ! vpuenc_hevc ! v4l2sink device=/dev/video10 sync=false"
    # pipeline_str = f"rtspsrc location={rtsp_url} latency=0 ! rtph264depay ! h264parse ! vpudec ! v4l2sink device=/dev/video10 sync=false"


    print(f"Creating pipeline: {pipeline_str}")
    pipeline = Gst.parse_launch(pipeline_str)
    # caps = Gst.Caps.from_string("video/x-h264,stream-format=byte-stream,alignment=au")
    # caps = Gst.Caps.from_string("video/x-raw,format=NV12,width=1080,height=720,colorimetry=bt709")
    # filter = pipeline.get_by_name("filter")
    # filter.set_property("caps", caps)



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

