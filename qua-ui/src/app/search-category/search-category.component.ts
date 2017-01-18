import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { CategoryService } from '../services/category.service';
import { ICategory } from '../interfaces/category.interface';

@Component({
  selector: 'app-search-category',
  templateUrl: './search-category.component.html',
  styleUrls: ['./search-category.component.less']
})
export class SearchCategoryComponent implements OnInit {
  categories: ICategory[];
  sfHide: boolean = true;

  constructor(
    private categoryService: CategoryService
  ) { }

  edit(category: ICategory) {
    category['isEdit'] = true;
    category['temp'] = category.name;
  }

  cancel(event: MouseEvent, category: ICategory) {
    event.cancelBubble = true;
    category['isEdit'] = false;
    category.name = category['temp'];
  }

  add(name: string) {
    this.categoryService.addCategory(name)
      .then(() => {
        this.get();
      });
  }

  delete(id: number) {
    this.categoryService.deleteCategory(id)
      .then(() => {
        this.get();
      });
  }

  update(event: MouseEvent, category: ICategory) {
    event.cancelBubble = true;
    category['isEdit'] = false;
    this.categoryService.putCategory(category.id, category.name)
      .then(() => {
        this.get();
      });
  }

  get() {
    this.categoryService.getCategories()
      .then((categories: ICategory[]) => {
        this.categories = categories;
      });
  }

  ngOnInit() {
    this.get();
  }
}
