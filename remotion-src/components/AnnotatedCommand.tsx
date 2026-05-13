import React from "react";
import { useCurrentFrame } from "remotion";
import { windowProgress } from "../utils/timing";

interface Part {
  token: string;
  label: string;
}

interface Props {
  parts: Part[];
  revealPerSecond?: number;
}

export const AnnotatedCommand: React.FC<Props> = ({ parts, revealPerSecond = 1 }) => {
  const frame = useCurrentFrame();
  const revealed = Math.floor(windowProgress(frame, 0, parts.length * 30 / revealPerSecond) * parts.length);

  return (
    <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 26, color: "#CDD6F4" }}>
      <div style={{ display: "flex", gap: 24, flexWrap: "wrap", marginBottom: 16 }}>
        {parts.map((p, i) => (
          <span
            key={i}
            style={{ color: i < revealed ? "#CBA6F7" : "#585B70", transition: "color 0.3s" }}
          >
            {p.token}
          </span>
        ))}
      </div>
      <div style={{ display: "flex", gap: 24, flexWrap: "wrap" }}>
        {parts.map((p, i) => (
          <span
            key={i}
            style={{
              fontSize: 16,
              color: i < revealed ? "#A6E3A1" : "transparent",
              minWidth: p.token.length * 15,
              transition: "color 0.3s",
            }}
          >
            {p.label}
          </span>
        ))}
      </div>
    </div>
  );
};
