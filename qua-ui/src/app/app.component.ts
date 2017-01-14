import { Component, OnInit } from '@angular/core';

import { AuthService } from './auth.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.less']
})
export class AppComponent implements OnInit {
  isAuth: boolean;
  sfHide: boolean = false;

  constructor(private authService: AuthService) {}

  onActivate(event): void {
    if (typeof event.sfHide !== 'undefined') {
      this.sfHide = event.sfHide;
    } else {
      this.sfHide = false;
    }
  }

  ngOnInit() {
    this.authService.isAuth$.subscribe((isAuth: boolean) => {
      this.isAuth = isAuth;
    });
  }
}
