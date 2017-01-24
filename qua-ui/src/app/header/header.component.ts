import { Component, Input } from '@angular/core';

import { AuthService } from '../services/auth.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.less']
})
export class HeaderComponent {
  @Input() isAuth: boolean;

  constructor(
    private authService: AuthService
  ) { }

  exit() {
    this.authService.logout();
  }
}
