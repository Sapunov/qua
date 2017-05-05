export interface IHits {
  id: number;
  title: string;
  snippet: string;
  image: string;
  score: number;
  keywords: string[];
  url_params: {
    qid: number;
    shid: number;
    token: string;
  };
  url?: string;
  is_external?: boolean;
  resource?: string;
};

export interface ISearchResult {
  hits: IHits[];
  query: string;
  query_was_corrected: string;
  total: number;
  used_query: string;
  took: number;
  pagination: {
    next: string | null;
    prev: string | null;
  };
};

export interface ISearchInfo {
  took: number;
  total: number;
};

export interface ISearchParams {
  query: string;
  offset: string;
  limit: string;
  spelling?: string;
};

export interface IGetSuggests {
  query: string;
  limit?: string;
};

export interface ISuggest {
  text: string;
  rate: number;
  quick_ans: string;
};
