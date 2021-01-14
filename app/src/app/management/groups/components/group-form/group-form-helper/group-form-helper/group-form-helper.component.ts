import { Component, Input, OnInit } from '@angular/core';
import { Right } from '../../../../../models/right';

@Component({
  selector: 'cmdb-group-form-helper',
  templateUrl: './group-form-helper.component.html',
  styleUrls: ['./group-form-helper.component.scss']
})
export class GroupFormHelperComponent implements OnInit {

  presetList = [];

  @Input() public rights: Array<Right> = [];

  public minRights: any[] = [];

  constructor() { }

  ngOnInit() {
    this.minRights = this.rights.filter(right => right.name.includes('view') && (right.name.includes('framework') ||
      right.name.includes('user-management')));
    this.presetList.push({
        name: 'Read-Only',
        value: this.minRights
      },
      {
        name: 'Object-Write',
        value: this.rights.filter(right => right.name.includes('object.add')).concat(this.minRights)
      },
      {
        name: 'Administrator',
        value: this.rights.filter(right => right.name.includes('base.*'))
      }
    );
  }
}
