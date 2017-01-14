import { Component, Input } from '@angular/core';

import { Router } from '@angular/router';
import { AuthService } from '../auth.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.less']
})
export class HeaderComponent {
  @Input() isAuth: boolean;

  constructor(
    private router: Router,
    private authService: AuthService
  ) { }

  exit() {
    this.authService.logout();
    this.router.navigate(['/auth']);
  }
}
