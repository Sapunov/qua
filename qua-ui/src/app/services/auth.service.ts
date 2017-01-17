import { Subject } from 'rxjs/Subject';
import { Injectable } from '@angular/core';
import { Headers, Http, RequestOptions } from '@angular/http';
import { CanActivate, Router } from '@angular/router';

import { IResponse } from '../interfaces/response.interface';

import { URLS } from '../../environments/const';

@Injectable()
export class AuthService implements CanActivate {
  private isAuthSource = new Subject<boolean>();

  isAuth$ = this.isAuthSource.asObservable();

  isAuth: boolean;
  token: string;

  constructor(
    private http: Http,
    private router: Router) { }

  canActivate() {
    this.isAuth = this.checkAuth();
    if (!this.isAuth) {
      this.router.navigate(['auth']);
      return false;
    }
    return true;
  }

  auth(username: string, password: string): Promise<any> {
    let data: any  = {
      username,
      password
    };
    let headers = new Headers({
      'Content-type': 'application/json'
    });
    let options = new RequestOptions({
      headers: headers
    });
    return this.http.post(URLS.auth, JSON.stringify(data), options)
      .toPromise()
      .then((response: any) => {
        return response.json() as IResponse;
      })
      .then((response: IResponse) => {
        if (!response.ok) {
          throw response.error;
        }
        this.token = response.response.token;
        this.isAuth = true;
        localStorage.setItem('token', response.response.token);
        return true;
      })
      .catch(this.handleError);
  }

  logout(): void {
    localStorage.removeItem('token');
  }

  checkAuth(): boolean {
    let token: string = localStorage.getItem('token');
    let isAuth: boolean = Boolean(token);
    this.isAuthSource.next(isAuth);
    return isAuth;
  }

  private handleError(error: any): Promise<any> {
    console.error('An error occurred', error); // for demo purposes only
    return Promise.reject(error.message || error);
  }
}
