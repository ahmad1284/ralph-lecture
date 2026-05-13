import React from "react";
import { useCurrentFrame, interpolate } from "remotion";
import { TerminalWindow } from "../components/TerminalWindow";

interface Props {
  section: {
    title: string;
    visual_content?: { description?: string };
  };
}

export const Diff: React.FC<Props> = ({ section }) => {
  const frame = useCurrentFrame();
  const rightOpacity = interpolate(frame, [30, 60], [0, 1], { extrapolateRight: "clamp" });
  const desc = section.visual_content?.description ?? "";
  const [before, after] = desc.includes("→") ? desc.split("→") : [desc, desc];

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        background: "#0F1117",
        display: "flex",
        flexDirection: "column",
        padding: "60px 60px",
        boxSizing: "border-box",
      }}
    >
      <div style={{ fontSize: 38, fontFamily: "'Inter', sans-serif", color: "#CBA6F7", marginBottom: 32, fontWeight: 600 }}>
        {section.title}
      </div>
      <div style={{ display: "flex", gap: 32, flex: 1 }}>
        <div style={{ flex: 1 }}>
          <div style={{ color: "#F38BA8", marginBottom: 8, fontSize: 22 }}>Before</div>
          <TerminalWindow>
            <pre style={{ color: "#F38BA8", margin: 0, fontSize: 20, whiteSpace: "pre-wrap" }}>{before.trim()}</pre>
          </TerminalWindow>
        </div>
        <div style={{ flex: 1, opacity: rightOpacity }}>
          <div style={{ color: "#A6E3A1", marginBottom: 8, fontSize: 22 }}>After</div>
          <TerminalWindow>
            <pre style={{ color: "#A6E3A1", margin: 0, fontSize: 20, whiteSpace: "pre-wrap" }}>{after.trim()}</pre>
          </TerminalWindow>
        </div>
      </div>
    </div>
  );
};
