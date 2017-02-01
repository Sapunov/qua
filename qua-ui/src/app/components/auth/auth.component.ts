import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { Router } from '@angular/router';

import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-auth',
  templateUrl: './auth.component.html',
  styleUrls: ['./auth.component.less']
})
export class AuthComponent implements OnInit {
  sfHide: boolean;
  username: string;
  password: string;
  loading: boolean;

  constructor(
    private authService: AuthService,
    private router: Router) {
    this.sfHide = true;
    this.loading = false;
    }

  onSubmit() {
    this.loading = true;
    this.authService.auth(this.username, this.password)
      .then(() => {
        this.loading = false;
        this.router.navigateByUrl(this.authService.getRedirect());
      })
      .catch(err => {
        this.loading = false;
      });
  }
  ngOnInit() {
    if (this.authService.checkAuth()) {
      this.router.navigate(['/']);
    }
  }
}
