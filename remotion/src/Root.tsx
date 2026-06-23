import { Composition, Folder } from "remotion";
import { IntroVideo } from "./IntroVideo";

export const RemotionRoot = () => {
  return (
    <Folder name="agrisage-intro">
      <Composition
        id="IntroVideo"
        component={IntroVideo}
        durationInFrames={103 * 30} // 103秒 @ 30fps (匹配配音音频)
        fps={30}
        width={1920}
        height={1080}
      />
    </Folder>
  );
};
