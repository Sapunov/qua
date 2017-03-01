import 'rxjs/add/operator/switchMap';
import { Component, OnInit, OnDestroy, ViewChild, ElementRef, AfterViewInit } from '@angular/core';
import { ActivatedRoute, Params, Router, NavigationExtras } from '@angular/router';
import { FormGroup } from '@angular/forms';
import { NgProgressService } from 'ng2-progressbar';

import { MarkdownComponent } from '../markdown/markdown.component';

import { QuestionService } from '../../services/question.service';

import { IQuestion, INewQuestion, IAnswer, ITempQuestion } from '../../interfaces/question.interface';

@Component({
  selector: 'app-search-add',
  templateUrl: './search-add.component.html',
  styleUrls: ['./search-add.component.less']
})
export class SearchAddComponent implements OnInit, OnDestroy, AfterViewInit {
  @ViewChild(MarkdownComponent) private mde: MarkdownComponent;
  @ViewChild('inputTitle') private inputTitle: ElementRef;

  private sfHide = true;
  private title = '';
  private keyword = '';
  private answer = '';
  private id = 0;
  private keywords: string[] = [];
  private cache: ITempQuestion = null;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private questionService: QuestionService,
    private pbService: NgProgressService,
  ) { }

  onSubmit(form: FormGroup): void {
    if (form.invalid) {
      return;
    }
    this.questionService.setCacheNewQuestion({
      title: this.title,
      keywords: this.keywords,
      answer: this.mde.getValue(),
      id: this.id
    });
    let data: INewQuestion = {
      title: this.title,
      keywords: this.keywords,
      answer: { raw: this.mde.getValue() }
    };
    if (this.id) {
      this.edit(this.id, data);
    } else {
      this.add(data);
    }
  }


  edit(id: number, data: INewQuestion) {
    this.pbService.start();
    this.questionService.editQuestion(id, data)
      .then((que: IQuestion) => {
        this.questionService.clearCacheNewQuestion();
        this.pbService.done();
        this.router.navigate([`questions/${que.id}`]);
      })
      .catch(err => {
        this.pbService.done();
      });
  }

  add(data: INewQuestion) {
    this.pbService.start();
    this.questionService.addQuestion(data)
      .then((que: IQuestion) => {
        this.questionService.clearCacheNewQuestion();
        this.pbService.done();
        this.router.navigate([`questions/${que.id}`]);
      })
      .catch(err => {
        this.pbService.done();
      });
  }

  onBackspace(event: KeyboardEvent) {
    if (this.keywords.length && !this.keyword) {
      this.keywords.pop();
    }
  }

  onKeypress() {
    this.questionService.setCacheNewQuestion({
      title: this.title,
      keywords: this.keywords,
      answer: this.mde.getValue(),
      id: this.id
    });
    this.cache = null;
  }

  addKeyword() {
    let checkKeywords = this.keywords.indexOf(this.keyword);
    if (this.keyword && checkKeywords) {
      this.keywords.push(this.keyword);
    }
  }

  delKeyword(keyword: string) {
    let index = this.keywords.indexOf(keyword);
    if (index !== -1) {
      this.keywords.splice(index, 1);
    }
  }

  continueChanges() {
    this.title = this.cache.title;
    this.keywords = this.cache.keywords;
    this.answer = this.cache.answer;
    this.id = this.cache.id;
    this.mde.setValue(this.cache.answer);
    this.cache = null;
  }

  clearChanges() {
    this.questionService.clearCacheNewQuestion();
    this.cache = null;
  }

  ngOnInit() {
    let question = this.questionService.getQuestionForEdit();
    this.cache = this.questionService.getCacheNewQuestion();
    if (question) {
      this.title = question.title;
      this.keywords = question.keywords;
      this.answer = question.answer;
      this.id = question.id;
    }
  }

  ngAfterViewInit() {
    this.inputTitle.nativeElement.focus();
  }

  ngOnDestroy() {
    this.questionService.question = null;
  }
}
