// define all custom types and interfaces here

export type InputNewsType = {
  category: "text" | "url";
  content: string;
};

export type InputMessageType = {
  message: string;
};

export type OutputNewsType = {
  label: "real" | "fake" | "neutral";
  relatedNews?: FetchedNewsType[];
};

export type FetchedNewsType = {
  link: string;
  source: string;
};

export type TeamMembers = {
  name: string;
  email: string;
  linkedinUrl: string;
};
