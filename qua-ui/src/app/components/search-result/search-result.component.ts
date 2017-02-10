import 'rxjs/add/operator/switchMap';
import { Component, OnInit, OnDestroy } from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';
import { Router, NavigationExtras } from '@angular/router';
import { NgProgressService } from 'ng2-progressbar';

import { QuestionService } from '../../services/question.service';
import { SearchService } from '../../services/search.service';
import { IHits, ISearchResult, ISearchParams } from '../../interfaces/search-hits.interface';

import { URLS } from '../../../environments/const';

@Component({
  selector: 'app-search-result',
  templateUrl: './search-result.component.html',
  styleUrls: ['./search-result.component.less']
})
export class SearchResultComponent implements OnInit, OnDestroy {
  result: ISearchResult;
  hits: IHits[];
  prevResult: string;
  nextResult: string;
  url: string;

  constructor(
    private search: SearchService,
    private route: ActivatedRoute,
    private router: Router,
    private pbService: NgProgressService,
    private questionService: QuestionService
  ) {
    this.prevResult = null;
    this.nextResult = null;
    this.hits = [];
    this.url = '/search';
  }

  addQuestion(title: string): void {
    this.questionService.addQuestionWithTitle(title);
    this.router.navigate(['add']);
  }

  searchSpellOrigin() {
    let params: NavigationExtras = {
      queryParams: {
        query: this.result.query,
        spelling: 0
      }
    };
    this.router.navigate(['/search'], params);
  }

  ngOnInit() {
    this.route.queryParams
      .switchMap((params: ISearchParams) => {
        window.scrollTo(0, 0);
        this.pbService.start();
        return this.search.goSearch(params)
          .catch(err => null);
      })
      .subscribe((result: ISearchResult) => {
        this.pbService.done();
        if (result) {
          this.hits = result.hits;
          this.prevResult = result.pagination.prev;
          this.nextResult = result.pagination.next;
          return this.result = result;
        } else {
          this.hits = [];
          this.result = null;
        }
      });
  }

  ngOnDestroy() {
    this.search.searchInfo.next(null);
  }
}
