import 'rxjs/add/operator/switchMap';
import { Component, OnInit, OnDestroy, ViewChild, ElementRef, AfterViewInit } from '@angular/core';
import { ActivatedRoute, Params, Router, NavigationExtras } from '@angular/router';
import { FormGroup } from '@angular/forms';

import { MarkdownComponent } from '../markdown/markdown.component';

import { ErrorService } from '../services/error.service';
import { QuestionService } from '../services/question.service';

import { IQuestion, INewQuestion, IAnswer } from '../interfaces/question.interface';

@Component({
  selector: 'app-search-add',
  templateUrl: './search-add.component.html',
  styleUrls: ['./search-add.component.less']
})
export class SearchAddComponent implements OnInit, OnDestroy, AfterViewInit {
  @ViewChild(MarkdownComponent) private mde: MarkdownComponent;
  @ViewChild('inputTitle') private inputTitle: ElementRef;

  loading: boolean = false;

  question: IQuestion | INewQuestion;
  isReply: boolean = false;
  sfHide: boolean = true;
  title: string = '';
  keywords: string[] = [];
  keyword: string;
  answer: any = {
    raw: ''
  };

  constructor(
    private errorService: ErrorService,
    private route: ActivatedRoute,
    private router: Router,
    private questionService: QuestionService,
  ) {  }

  onSubmit(form: FormGroup): void {
    if (form.invalid) {
      return;
    }
    this.answer = { raw: this.mde.getValue() };
    if (this.isReply) {
      this.edit(this.question['id']);
    } else {
      this.add();
    }
  }

  edit(id: number) {
    let data: INewQuestion = {
      title: this.title,
      keywords: this.keywords,
      answer: this.answer
    };
    this.questionService.editQuestion(id, data)
      .then((que: IQuestion) => {
        this.router.navigate([`questions/${que.id}`]);
      })
      .catch(err => this.errorService.viewError(err));
  }

  add() {
    let data: INewQuestion = {
      title: this.title,
      keywords: this.keywords,
    };
    this.loading = true;
    if (this.answer.raw) {
      data.answer = this.answer;
    }
    this.questionService.addQuestion(data)
      .then((que: IQuestion) => {
        this.router.navigate([`questions/${que.id}`]);
      })
      .catch(err => this.errorService.viewError(err))
      .then(() => {
        this.loading = false;
      });
  }

  addKeyword(form: FormGroup) {
    if (this.keyword && form.valid) {
      this.keywords.push(this.keyword);
    }
  }

  delKeyword(index: number) {
    this.keywords.splice(index, 1);
  }

  ngOnInit() {
    let question = this.questionService.question;
    if (question && !question['new']) {
      this.title = question.title || this.title;
      this.keywords = question.keywords.slice() || this.keywords;
      this.answer = question.answer ? Object.assign({}, question.answer) : this.answer;
      this.isReply = question.reply;
      this.question = question;
    } else if (question) {
      this.title = question.title || this.title;
    }
  }

  ngAfterViewInit() {
    this.inputTitle.nativeElement.focus();
  }

  ngOnDestroy() {
    this.questionService.question = null;
  }
}
