import { Injectable }    from '@angular/core';
import { Headers, Http, RequestOptions, URLSearchParams } from '@angular/http';
import { URLS } from '../../environments/const';

import 'rxjs/add/operator/toPromise';

import { ErrorService } from './error.service';

import { ISearchResult } from '../interfaces/search-hits.interface';
import { IResponse } from '../interfaces/response.interface';

@Injectable()
export class SearchService {

  private headers = new Headers({
    'Content-type': 'application/json',
    Authorization: `JWT ${localStorage.getItem('token')}`
  });

  constructor(
    private errorService: ErrorService,
    private http: Http) { }

  goSearch(query: string): Promise<ISearchResult> {
    let options = new RequestOptions({
      headers: this.headers,
      withCredentials: true
    });
    let param: URLSearchParams = new URLSearchParams;
    param.set('query', query);
    options.search = param;
    return this.http.get(`${URLS.search}`, options)
      .toPromise()
      .then((response: any) => {
        return response.json() as IResponse;
      })
      .then((response: IResponse) => {
        if (!response.ok) {
          throw response.error;
        }
        return response.response;
      })
      .catch(this.handleError);
  }

  private handleError = (error) => {
    this.errorService.handleError(error);
  }
}
