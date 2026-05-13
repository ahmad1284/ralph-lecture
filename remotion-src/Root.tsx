import React from "react";
import { Composition } from "remotion";
import { TextCard } from "./compositions/TextCard";
import { Terminal } from "./compositions/Terminal";
import { Split } from "./compositions/Split";
import { FlagExplainer } from "./compositions/FlagExplainer";
import { Diff } from "./compositions/Diff";
import { secondsToFrames } from "./utils/timing";

interface SectionProps {
  index: number;
  title: string;
  narration: string;
  visual_type: "text" | "equation" | "graph" | "diagram" | "proof";
  visual_content: {
    latex?: string;
    description?: string;
    axes?: { x: string; y: string };
  };
  estimated_duration_seconds: number;
}

const SceneRouter: React.FC<{ section: SectionProps }> = ({ section }) => {
  const desc = section.visual_content?.description ?? "";
  if (section.visual_type === "text") return <TextCard section={section} />;
  if (desc.includes("[") && desc.includes("]")) return <FlagExplainer section={section} />;
  if (desc.includes("→")) return <Diff section={section} />;
  if (desc.startsWith("$") && section.narration.includes(".")) return <Split section={section} />;
  if (desc.startsWith("$") || desc.toLowerCase().includes("command")) return <Terminal section={section} />;
  return <TextCard section={section} />;
};

const defaultSection: SectionProps = {
  index: 0,
  title: "Preview",
  narration: "This is a preview of the ralph-lecturer Remotion composition.",
  visual_type: "text",
  visual_content: { description: "Loaded via ralph-lecturer pipeline" },
  estimated_duration_seconds: 10,
};

export const RemotionRoot: React.FC = () => (
  <>
    <Composition
      id="SceneComp"
      component={({ section }: { section: SectionProps }) => <SceneRouter section={section} />}
      durationInFrames={secondsToFrames(defaultSection.estimated_duration_seconds)}
      fps={30}
      width={1920}
      height={1080}
      defaultProps={{ section: defaultSection }}
      calculateMetadata={async ({ props }) => ({
        durationInFrames: secondsToFrames(
          (props as { section: SectionProps }).section.estimated_duration_seconds
        ),
      })}
    />
  </>
);
