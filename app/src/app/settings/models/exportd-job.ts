/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2024 becon GmbH
*
* This program is free software: you can redistribute it and/or modify
* it under the terms of the GNU Affero General Public License as
* published by the Free Software Foundation, either version 3 of the
* License, or (at your option) any later version.
*
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU Affero General Public License for more details.

* You should have received a copy of the GNU Affero General Public License
* along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

export class ExportdJob {

  // tslint:disable: variable-name
  private readonly _id?: string;
  public public_id: number;
  public name: string;
  public label: string;
  public description: string;
  public active: boolean;
  public author_id: number;
  public author_name: string;
  public last_execute_date: any;
  public sources: [];
  public destination: [];
  public variables: [];
  public scheduling: any;
  public running: boolean;
  public state: any;
  public exportd_type: string;
  // tslint:enable
}
