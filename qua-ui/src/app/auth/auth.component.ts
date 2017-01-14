import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { Router } from '@angular/router';

import { AuthService } from '../auth.service';

@Component({
  selector: 'app-auth',
  templateUrl: './auth.component.html',
  styleUrls: ['./auth.component.less']
})
export class AuthComponent implements OnInit {
  username: string;
  password: string;

  constructor(
    private authService: AuthService,
    private router: Router) { }

  onSubmit() {
    this.authService.auth(this.username, this.password)
      .then(res => {
        this.router.navigate(['/']);
      });
  }
  ngOnInit() {
    if (this.authService.checkAuth()) {
      this.router.navigate(['/']);
    }
  }
}
