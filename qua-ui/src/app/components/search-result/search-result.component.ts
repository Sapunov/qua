import 'rxjs/add/operator/switchMap';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';
import { Router, NavigationExtras } from '@angular/router';

import { QuestionService } from '../../services/question.service';
import { SearchService } from '../../services/search.service';
import { IHits, ISearchResult } from '../../interfaces/search-hits.interface';

@Component({
  selector: 'app-search-result',
  templateUrl: './search-result.component.html',
  styleUrls: ['./search-result.component.less']
})
export class SearchResultComponent implements OnInit {
  result: ISearchResult;
  hits: IHits[];
  loading: boolean;

  constructor(
    private search: SearchService,
    private route: ActivatedRoute,
    private router: Router,
    private questionService: QuestionService
  ) {
    this.loading = false;
  }

  addQuestion(title: string): void {
    this.questionService.question = {
      title
    };
    this.router.navigate(['add']);
  }

  getQuestion(hit: IHits): void {
    let params: NavigationExtras = {
      queryParams: hit.url_params
    };
    this.router.navigate([`questions/${hit.id}`], params);
  }

  ngOnInit() {
    this.route.queryParams
      .switchMap((params: Params) => {
        this.loading = true;
        return this.search.goSearch(params['query'])
          .catch(err => null);
      })
      .subscribe((result: ISearchResult) => {
        this.loading = false;
        if (result) {
          this.hits = result.hits;
          return this.result = result;
        }
      });
  }
}