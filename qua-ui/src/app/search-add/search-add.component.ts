import 'rxjs/add/operator/switchMap';
import { Component, OnInit, ViewChild  } from '@angular/core';
import { ActivatedRoute, Params, Router, NavigationExtras } from '@angular/router';

import { MarkdownComponent } from '../markdown/markdown.component';

import { QuestionService } from '../question.service';

import { IQuestion, INewQuestion } from '../question.interface';

@Component({
  selector: 'app-search-add',
  templateUrl: './search-add.component.html',
  styleUrls: ['./search-add.component.less']
})
export class SearchAddComponent implements OnInit {
  @ViewChild(MarkdownComponent) private mde: MarkdownComponent;

  isReply: boolean = false;
  question: INewQuestion;
  sfHide: boolean = true;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private questionService: QuestionService
  ) { }

  onSubmit(question: string): void {
    let raw: string = this.mde.getValue();
    if (this.isReply) {
      this.edit(this.question['id'], question, raw);
    } else {
      this.add(question, raw);
    }
  }

  edit(id: number, title: string, raw: string) {
    let data = {
      title,
      answer: {
        raw
      }
    };
    this.questionService.editQuestion(id, data)
      .then((que: IQuestion) => {
        this.router.navigate([`questions/${que.id}`]);
      });
  }

  add(title: string, raw: string) {
    let data = {
      title,
      answer: {
        raw
      }
    };
    this.questionService.addQuestion(data)
      .then((newQue: IQuestion) => {
        this.router.navigate([`questions/${newQue.id}`]);
      });
  }

  ngOnInit() {
    this.route.queryParams.subscribe((params: INewQuestion) => {
      if (params.reply) {
        this.isReply = true;
      }
      this.question = params;
    });
  }
}
