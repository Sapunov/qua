import 'rxjs/add/operator/switchMap';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';
import { Location } from '@angular/common';
import { Router, NavigationExtras } from '@angular/router';

import { SearchService } from '../search.service';
import { IHits, ISearchResult } from '../search-hits.interface';

@Component({
  selector: 'app-search-result',
  templateUrl: './search-result.component.html',
  styleUrls: ['./search-result.component.less']
})
export class SearchResultComponent implements OnInit {
  result: ISearchResult;
  hits: IHits[];
  total: number = 0;

  constructor(
    private search: SearchService,
    private route: ActivatedRoute,
    private router: Router,
    private location: Location
  ) { }

  addQuestion(question: string): void {
    let params: NavigationExtras = {
      queryParams: {
        title: question
      }
    };
    this.router.navigate(['add'], params);
  }

  getQuestion(data: any, id: number): void {
    let params: NavigationExtras = {
      queryParams: data
    };
    this.router.navigate([`questions/${id}`], params);
  }

  ngOnInit() {
    this.route.queryParams
      .switchMap((params: Params) => {
        return this.search.goSearch(params['query'] || '');
      })
      .subscribe(result => {
        this.hits = result.hits;
        return this.result = result;
      });
  }
}
