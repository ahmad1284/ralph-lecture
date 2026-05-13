import React from "react";
import { useCurrentFrame } from "remotion";
import { windowProgress } from "../utils/timing";

interface Props {
  text: string;
  startFrame?: number;
  charsPerSecond?: number;
  color?: string;
  prefix?: string;
}

export const TypewriterText: React.FC<Props> = ({
  text,
  startFrame = 0,
  charsPerSecond = 30,
  color = "#A6E3A1",
  prefix = "$ ",
}) => {
  const frame = useCurrentFrame();
  const elapsed = Math.max(0, frame - startFrame);
  const charsVisible = Math.floor(elapsed * (charsPerSecond / 30));
  const visible = text.slice(0, charsVisible);

  return (
    <div style={{ color, whiteSpace: "pre-wrap", wordBreak: "break-all" }}>
      <span style={{ color: "#CBA6F7" }}>{prefix}</span>
      {visible}
      {charsVisible < text.length && (
        <span style={{ opacity: Math.floor(elapsed / 15) % 2 === 0 ? 1 : 0 }}>▌</span>
      )}
    </div>
  );
};
