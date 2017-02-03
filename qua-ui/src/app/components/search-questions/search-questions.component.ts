import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { QuestionService } from '../../services/question.service';
import { IQuestion } from '../../interfaces/question.interface';

@Component({
  selector: 'app-search-questions',
  templateUrl: './search-questions.component.html',
  styleUrls: ['./search-questions.component.less']
})
export class SearchQuestionsComponent implements OnInit {
  questions: IQuestion[] = [];
  loading: boolean;

  constructor(
    private questionService: QuestionService,
    private router: Router
  ) {
    this.loading = false;
  }

  getQuestion(id: number) {
    this.router.navigate([`questions/${id}`]);
  }

  ngOnInit() {
    if (this.questionService.questions) {
      this.questions = this.questionService.questions;
    } else {
      this.loading = true;
      this.questionService.getQuestions()
        .then((questions: IQuestion[]) => {
          this.loading = false;
          this.questions = questions;
        })
        .catch(err => {
          this.loading = false;
        });
    }
  }
}
