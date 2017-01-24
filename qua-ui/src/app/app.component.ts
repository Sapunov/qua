import { Component, OnInit, OnDestroy } from '@angular/core';

import { AuthService } from './services/auth.service';
import { Subscription }   from 'rxjs/Subscription';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.less']
})
export class AppComponent implements OnInit, OnDestroy {
  isAuth: boolean;
  sfHide: boolean = false;
  sub: Subscription;

  constructor(private authService: AuthService) {

  }

  onActivate(event): void {
    if (typeof event.sfHide !== 'undefined') {
      this.sfHide = event.sfHide;
    } else {
      this.sfHide = false;
    }
  }

  ngOnInit() {
    this.sub = this.authService.isAuth$.subscribe((isAuth: boolean) => {
      this.isAuth = isAuth;
    });
  }

  ngOnDestroy() {
    this.sub.unsubscribe();
  }
}
