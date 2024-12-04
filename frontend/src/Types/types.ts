// define all custom types and interfaces here

export type InputNewsType = {
  category: "text" | "url";
  content: string;
};

export type OutputNewsType = {
  label: "real" | "fake";
};
