import { Component, Input, OnInit } from '@angular/core';
import { ConfigEditBaseComponent } from '../config.edit';

@Component({
  selector: 'cmdb-check-field-edit',
  templateUrl: './check-field-edit.component.html',
  styleUrls: ['./check-field-edit.component.scss']
})
export class CheckFieldEditComponent extends ConfigEditBaseComponent implements OnInit {

  @Input() groupList: any;
  @Input() userList: any;
  public options = [];

  constructor() {
    super();
    this.options.push({
      name: 'option-1',
      label: 'Option 1'
    });
  }

  public ngOnInit(): void {
    this.data.options = this.options;
  }

}
