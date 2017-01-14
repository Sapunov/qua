import { Injectable }    from '@angular/core';
import { Headers, Http, RequestOptions, URLSearchParams } from '@angular/http';
import { environment } from '../environments/environment';

import 'rxjs/add/operator/toPromise';

import { ICategory } from './category.interface';
import { IResponse } from './response.interface';

@Injectable()
export class CategoryService {

  private headers = new Headers({
    'Content-type': 'application/json',
    Authorization: `JWT ${localStorage.getItem('token')}`
  });

  constructor(private http: Http) { }

  addCategory(name: string) {
    let data = {
      name
    };
    let options = new RequestOptions({
      headers: this.headers,
      withCredentials: true
    });
    return this.http.post(`${environment.urls.category}`, JSON.stringify(data), options)
      .toPromise()
      .then((response: any) => {
        return response.json() as IResponse;
      })
      .then((response: IResponse) => {
        if (!response.ok) {
          throw response;
        }
        return response.response as ICategory[];
      })
      .catch(this.handleError);
  }

  getCategories() {
    let options = new RequestOptions({
      headers: this.headers,
      withCredentials: true
    });
    return this.http.get(`${environment.urls.category}`, options)
      .toPromise()
      .then((response: any) => {
        return response.json() as IResponse;
      })
      .then((response: IResponse) => {
        if (!response.ok) {
          throw response;
        }
        return response.response as ICategory[];
      })
      .catch(this.handleError);
  }

  putCategory(id: number, name: string) {
    let data = {
      name
    };
    let options = new RequestOptions({
      headers: this.headers,
      withCredentials: true
    });
    return this.http.put(`${environment.urls.category}/${id}`, JSON.stringify(data), options)
      .toPromise()
      .then((response: any) => {
        return response.json() as IResponse;
      })
      .then((response: IResponse) => {
        console.log(response);
        if (!response.ok) {
          throw response;
        }
        return response.response as ICategory[];
      })
      .catch(this.handleError);
  }

  deleteCategory(id: number) {
    let options = new RequestOptions({
      headers: this.headers,
      withCredentials: true
    });
    return this.http.delete(`${environment.urls.category}/${id}`, options)
      .toPromise()
      .then((response: any) => {
        return response.json() as IResponse;
      })
      .then((response: IResponse) => {
        console.log(response);
        if (!response.ok) {
          throw response;
        }
        return response.response as ICategory[];
      })
      .catch(this.handleError);
  }

  private handleError(error: any): Promise<any> {
    console.error('An error occurred', error); // for demo purposes only
    return Promise.reject(error.message || error);
  }
}
