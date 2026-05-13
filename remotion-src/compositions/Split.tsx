import React from "react";
import { useCurrentFrame, interpolate } from "remotion";
import { TerminalWindow } from "../components/TerminalWindow";
import { TypewriterText } from "../components/TypewriterText";

interface Props {
  section: {
    title: string;
    narration: string;
    visual_content?: { description?: string };
    estimated_duration_seconds: number;
  };
}

export const Split: React.FC<Props> = ({ section }) => {
  const frame = useCurrentFrame();
  const desc = section.visual_content?.description ?? "";
  const command = desc.startsWith("$") ? desc.slice(1).trim() : desc;
  const bullets = section.narration.split(".").filter(Boolean).slice(0, 4);
  const visibleBullets = Math.min(bullets.length, Math.floor(frame / 60) + 1);
  const leftOpacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: "clamp" });

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        background: "#0F1117",
        display: "flex",
        alignItems: "center",
        padding: "60px 60px",
        boxSizing: "border-box",
        gap: 48,
      }}
    >
      <div style={{ flex: "0 0 38%", opacity: leftOpacity, fontFamily: "'Inter', sans-serif", color: "#CDD6F4" }}>
        <div style={{ fontSize: 36, fontWeight: 700, color: "#CBA6F7", marginBottom: 28 }}>
          {section.title}
        </div>
        {bullets.slice(0, visibleBullets).map((b, i) => (
          <div key={i} style={{ fontSize: 26, marginBottom: 16, lineHeight: 1.5 }}>
            • {b.trim()}.
          </div>
        ))}
      </div>
      <div style={{ flex: 1 }}>
        <TerminalWindow>
          <TypewriterText text={command} startFrame={20} />
        </TerminalWindow>
      </div>
    </div>
  );
};
