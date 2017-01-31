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
}

export interface ICategoryAssumptions {
  id: number;
  name: string;
  score: number;
}

export interface ISearchResult {
  query: string;
  query_was_corrected: string;
  used_query: string;
  hits: IHits[];
  total: number;
  category_assumptions?: ICategoryAssumptions[];
};
