import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'cmdb-sidebar-category',
  templateUrl: './sidebar-category.component.html',
  styleUrls: ['./sidebar.component.scss']
})
export class SidebarCategoryComponent implements OnInit {

  @Input() categoryData: any;
  constructor() { }

  ngOnInit() {

  }

}
