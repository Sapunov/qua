import { Injectable }    from '@angular/core';
import { Headers, Http, RequestOptions, URLSearchParams } from '@angular/http';
import { URLS, MIN_CHARS_FOR_SEARCH } from '../../environments/const';

import 'rxjs/add/operator/toPromise';

import { ErrorService } from './error.service';

import { ISearchResult } from '../interfaces/search-hits.interface';
import { IResponse } from '../interfaces/response.interface';

@Injectable()
export class SearchService {
  constructor(
    private errorService: ErrorService,
    private http: Http) { }

  goSearch(query: string): Promise<ISearchResult> {
    query = query || '';

    if (query.length < MIN_CHARS_FOR_SEARCH) {
      return Promise.resolve({
        query,
        total: 0,
        hits: []
      } as ISearchResult);
    }
    let options = this.makeOptions();
    let param: URLSearchParams = new URLSearchParams;
    param.set('query', query);
    options.search = param;
    return this.http.get(`${URLS.search}`, options)
      .toPromise()
      .then(this.promiseHandler)
      .catch(this.errorHandler);
  }

  private makeOptions() {
    let headers =  new Headers({
      'Content-type': 'application/json',
      Authorization: `JWT ${localStorage.getItem('token')}`
    });
    let options = new RequestOptions({
      headers: headers,
      withCredentials: true
    });
    return options;
  }

  private promiseHandler = (res: any): any => {
    let response = res.json() as IResponse;
    if (!response.ok) {
      throw response.error;
    }
    return response.response;
  }

  private errorHandler = (error) => {
    return this.errorService.handleError(error);
  }
}
