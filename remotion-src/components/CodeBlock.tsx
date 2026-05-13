import React from "react";

interface Props {
  code: string;
  language?: string;
}

export const CodeBlock: React.FC<Props> = ({ code }) => (
  <pre
    style={{
      margin: 0,
      fontFamily: "'JetBrains Mono', monospace",
      fontSize: 20,
      color: "#CDD6F4",
      background: "transparent",
      whiteSpace: "pre-wrap",
      wordBreak: "break-word",
    }}
  >
    {code}
  </pre>
);
