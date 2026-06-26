import { Composition, Folder } from "remotion";
import { IntroVideo } from "./IntroVideo";

export const RemotionRoot = () => {
  return (
    <Folder name="agrisage-intro">
      <Composition
        id="IntroVideo"
        component={IntroVideo}
        durationInFrames={115.5 * 30} // 115.5秒 @ 30fps（含转场静音缓冲）
        fps={30}
        width={1920}
        height={1080}
      />
    </Folder>
  );
};
