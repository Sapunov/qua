import { Subject } from 'rxjs/Subject';
import { Injectable, Injector } from '@angular/core';
import { Router } from '@angular/router';

import { IError } from '../interfaces/error.interface';
import { IResponse } from '../interfaces/response.interface';

@Injectable()
export class ErrorService {
  private error = new Subject<QuaError>();

  error$ = this.error.asObservable();

  constructor(
    private router: Router,
  ) {
  }

  viewError(err: QuaError) {
    console.error(err);
    console.error(err.stack);
    this.error.next(err);
  }

  handleError(response: any) {
    let error = null;
    if (response.status === 500) {
      error = new QuaError({
        error_msg: 'External error',
        error_code: 500
      });
      error.response = response;
    } else {
      let res;
      try {
        res = response.json() as IResponse;
      } catch (e) {
        res = {
          error: {
            error_msg: `This url: ${response.url} is ${response.statusText}`
          }
        };
      }
      if (!res.ok) {
        error = new QuaError(res.error);
      }
      if (response.status === 401) {
        // Необходимо выделить вызывать метод logout сервиса auth. Но пока хз как
        localStorage.removeItem('token');
        this.router.navigate(['auth']);
        // ----------------------------------------------------------------------
      }
      if (response.status === 403) {
        this.router.navigate(['/']);
      }
    }
    this.viewError(error);
    return Promise.reject(error);
  }
}

export class QuaError extends Error {
  name: string;
  code: number;
  constructor(ErrObj: IError) {
    super();
    this.name = ErrObj.error_msg;
    this.code = ErrObj.error_code || 0;
    if (Error.captureStackTrace) {
      Error.captureStackTrace(this, QuaError);
    } else {
      this.stack = (new Error()).stack;
    }
  }
}
