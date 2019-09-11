import { Component, OnDestroy, OnInit } from '@angular/core';
import { RenderResult } from '../../../models/cmdb-render';
import { Subject } from 'rxjs';
import { ObjectService } from '../../../services/object.service';
import { AuthService } from '../../../../auth/services/auth.service';

@Component({
  selector: 'cmdb-user-object-changed',
  templateUrl: './user-object-changed.component.html',
  styleUrls: ['./user-object-changed.component.scss']
})
export class UserObjectChangedComponent implements OnInit, OnDestroy {

  public changedObjects: RenderResult[] = [];
  public changedObjectsLength: number = 0;
  public issuedTokenTime: number;
  public dtOptions: DataTables.Settings = {};
  public dtTrigger: Subject<any> = new Subject();

  public constructor(private objectService: ObjectService, private authService: AuthService) {
    this.issuedTokenTime = this.authService.currentUserValue.token_issued_at;
  }

  public ngOnInit(): void {
    this.dtOptions = {
      ordering: true,
      order: [[3, 'desc']],
      language: {
        search: '',
        searchPlaceholder: 'Filter...'
      }
    };
    this.objectService.getChangedObjectsSince(this.issuedTokenTime).subscribe((objectList: RenderResult[]) => {
        this.changedObjects = objectList;
        this.changedObjectsLength = this.changedObjects.length;
      },
      (error) => {
        console.error(error);
        this.changedObjectsLength = 0;
        this.dtTrigger.next();
      },
      () => {
        this.dtTrigger.next();
      });
  }

  public ngOnDestroy(): void {
    this.dtTrigger.unsubscribe();
  }

}
