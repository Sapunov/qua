import { Component, Input } from '@angular/core';
import { Router } from '@angular/router';

import { QuestionService } from '../../services/question.service';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.less']
})
export class HeaderComponent {
  @Input() isAuth: boolean;

  constructor(
    private authService: AuthService,
    private questionService: QuestionService,
    private router: Router
  ) { }

  getQuestions() {
    this.questionService.clearCacheQuestions();
    this.router.navigate(['/questions']);
  }

  exit() {
    this.authService.logout();
  }
}
