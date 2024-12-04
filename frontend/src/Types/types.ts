// define all custom types and interfaces here

export type InputNewsType = {
  type: "text" | "url";
  data: string;
};

export type OutputNewsType = {
  label: "real" | "fake";
};
