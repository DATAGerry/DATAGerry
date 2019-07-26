import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'cmdb-check-field-edit',
  templateUrl: './check-field-edit.component.html',
  styleUrls: ['./check-field-edit.component.scss']
})
export class CheckFieldEditComponent implements OnInit {

  @Input() groupList: any;
  @Input() userList: any;
  @Input() data: any;
  public options = [];

  constructor() {
    this.options.push({
      name: 'option-1',
      label: 'Option 1'
    });
  }

  public ngOnInit(): void {
    this.data.options = this.options;
  }

}
