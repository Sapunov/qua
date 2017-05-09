import { Subject } from 'rxjs/Subject';
import { Subscription }   from 'rxjs/Subscription';
import { Component, OnInit, OnDestroy, HostListener } from '@angular/core';
import { Location } from '@angular/common';

import { AuthService } from './services/auth.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.less'],
})
export class AppComponent implements OnInit, OnDestroy {
  focusOnSf: Subject<{}> = new Subject();
  isAuth: boolean;
  sfHide: boolean;
  sub: Subscription;

  constructor(
    private location: Location,
    private authService: AuthService
  ) {
    this.sfHide = false;
  }

  @HostListener('document:keydown', ['$event'])
  onKeypdown(event: KeyboardEvent) {
    if (event.keyCode === 8) {
      this.focusOnSeacrh();
    }
  }
  @HostListener('document:keypress', ['$event'])
  onKeypress(event: KeyboardEvent) {
    this.focusOnSeacrh();
  }

  focusOnSeacrh() {
    if (!this.sfHide) {
      this.focusOnSf.next(true);
    }
  }

  onActivate(event): void {
    if (typeof event.sfHide !== 'undefined') {
      this.sfHide = event.sfHide;
    } else {
      this.sfHide = false;
    }
  }

  ngOnInit() {
    this.authService.checkToken();
    this.authService.setRedirect(this.location.path());
    this.sub = this.authService.isAuth$.subscribe((isAuth: boolean) => {
      this.isAuth = isAuth;
    });
  }

  ngOnDestroy() {
    this.sub.unsubscribe();
  }
}
