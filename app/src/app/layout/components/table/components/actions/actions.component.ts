import {Component, EventEmitter, Input, Output} from '@angular/core';
import {TableColumnAction} from '../../models/table-columns-action';
import {ApiCallService} from '../../../../../services/api-call.service';
import {ActivatedRoute, Router} from '@angular/router';
import {NgbModal} from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'cmdb-actions',
  templateUrl: './actions.component.html',
  styleUrls: ['./actions.component.scss']
})
export class ActionsComponent {

  @Input() data: TableColumnAction[];
  @Input() publicID: string = '';
  @Output() delete = new EventEmitter();

  constructor(private apiCallService: ApiCallService, private modalService: NgbModal,
              private activeRoute: ActivatedRoute, private router: Router) {
  }

  delObject(route: any) {
    this.delete.emit(route);
  }

}
