import { Subject } from 'rxjs/Subject';
import { Subscription }   from 'rxjs/Subscription';
import { Component, OnInit, OnDestroy, HostListener } from '@angular/core';

import { AuthService } from './services/auth.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.less'],
})
export class AppComponent implements OnInit, OnDestroy {
  focusOnSf: Subject<boolean> = new Subject();
  isAuth: boolean;
  sfHide: boolean = false;
  sub: Subscription;

  constructor(private authService: AuthService) {

  }

  @HostListener('document:keypress', ['$event'])
  onKeypress(event: KeyboardEvent) {
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
    this.sub = this.authService.isAuth$.subscribe((isAuth: boolean) => {
      this.isAuth = isAuth;
    });
  }

  ngOnDestroy() {
    this.sub.unsubscribe();
  }
}
