import React from "react";
import { useCurrentFrame, interpolate, Easing } from "remotion";

interface Props {
  section: {
    title: string;
    visual_content?: { description?: string };
    estimated_duration_seconds: number;
  };
}

export const TextCard: React.FC<Props> = ({ section }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 20], [0, 1], {
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.ease),
  });

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
        opacity,
        padding: "0 120px",
        boxSizing: "border-box",
      }}
    >
      <div
        style={{
          fontSize: 72,
          fontFamily: "'Inter', sans-serif",
          color: "#FFFFFF",
          fontWeight: 700,
          textAlign: "center",
          marginBottom: 24,
        }}
      >
        {section.title}
      </div>
      {section.visual_content?.description && (
        <div
          style={{
            fontSize: 34,
            fontFamily: "'Inter', sans-serif",
            color: "#CBA6F7",
            textAlign: "center",
          }}
        >
          {section.visual_content.description}
        </div>
      )}
    </div>
  );
};
