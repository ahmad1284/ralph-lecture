import React from "react";
import { AnnotatedCommand } from "../components/AnnotatedCommand";

interface Props {
  section: {
    title: string;
    visual_content?: { description?: string };
  };
}

function parseFlags(desc: string): Array<{ token: string; label: string }> {
  const parts = desc.split(/\s+/).filter(Boolean);
  return parts.map((p) => {
    const m = p.match(/^(.+?)\[(.+?)\]$/);
    if (m) return { token: m[1], label: m[2] };
    if (p.startsWith("-")) return { token: p, label: "flag" };
    return { token: p, label: "" };
  });
}

export const FlagExplainer: React.FC<Props> = ({ section }) => {
  const desc = section.visual_content?.description ?? section.title;
  const parts = parseFlags(desc);

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
        padding: "80px 100px",
        boxSizing: "border-box",
      }}
    >
      <div style={{ fontSize: 40, fontFamily: "'Inter', sans-serif", color: "#CBA6F7", marginBottom: 56, fontWeight: 600 }}>
        {section.title}
      </div>
      <AnnotatedCommand parts={parts} />
    </div>
  );
};
