import React from "react";
import { useCurrentFrame } from "remotion";
import { TerminalWindow } from "../components/TerminalWindow";
import { TypewriterText } from "../components/TypewriterText";
import { CodeBlock } from "../components/CodeBlock";

interface Props {
  section: {
    title: string;
    visual_content?: { description?: string; latex?: string };
    estimated_duration_seconds: number;
  };
}

export const Terminal: React.FC<Props> = ({ section }) => {
  const frame = useCurrentFrame();
  const desc = section.visual_content?.description ?? "";
  const command = desc.startsWith("$") ? desc.slice(1).trim() : desc;
  const outputVisible = frame > command.length + 15;

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        background: "#0F1117",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        padding: "60px 80px",
        boxSizing: "border-box",
      }}
    >
      <div
        style={{
          fontSize: 36,
          fontFamily: "'Inter', sans-serif",
          color: "#CBA6F7",
          marginBottom: 32,
          fontWeight: 600,
        }}
      >
        {section.title}
      </div>
      <TerminalWindow width="100%">
        <TypewriterText text={command} startFrame={10} />
        {outputVisible && (
          <div style={{ color: "#A6E3A1", marginTop: 8 }}>
            <CodeBlock code={`# output for: ${command}`} />
          </div>
        )}
      </TerminalWindow>
    </div>
  );
};
