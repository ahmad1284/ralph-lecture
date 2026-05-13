import React from "react";

interface Props {
  children: React.ReactNode;
  width?: string | number;
  height?: string | number;
}

const TRAFFIC = ["#FF5F57", "#FFBD2E", "#28C840"];

export const TerminalWindow: React.FC<Props> = ({ children, width = "100%", height = "auto" }) => (
  <div
    style={{
      width,
      height,
      borderRadius: 10,
      overflow: "hidden",
      fontFamily: "'JetBrains Mono', 'Fira Code', monospace",
      fontSize: 22,
      boxShadow: "0 8px 32px rgba(0,0,0,0.5)",
    }}
  >
    <div
      style={{
        background: "#313244",
        height: 36,
        display: "flex",
        alignItems: "center",
        paddingLeft: 14,
        gap: 8,
      }}
    >
      {TRAFFIC.map((c) => (
        <div key={c} style={{ width: 13, height: 13, borderRadius: "50%", background: c }} />
      ))}
    </div>
    <div
      style={{
        background: "#1E1E2E",
        padding: "20px 24px",
        minHeight: 120,
        color: "#CDD6F4",
        lineHeight: 1.7,
      }}
    >
      {children}
    </div>
  </div>
);
