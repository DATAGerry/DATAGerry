export interface APIPager {
  page: number;
  page_size: number;
  total_pages: number;
}

export interface APIPagination {
  current: string;
  first: string;
  prev: string;
  next: string;
  last: string;
}
