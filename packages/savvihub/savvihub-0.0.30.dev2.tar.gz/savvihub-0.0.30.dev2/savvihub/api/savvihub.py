import requests
import typing

import typer

from savvihub.api.types import PaginatedMixin, SavviHubListResponse, SavviHubFileObject, SavviHubDataset, \
    SavviHubKernelResource, SavviHubKernelImage, SavviHubExperiment, SavviHubProject, SavviHubWorkspace, SavviHubUser, \
    SavviHubExperimentLog, SavviHubSnapshot, SavviHubVolume, SavviHubExperimentMetric, SavviHubFileMetadata
from savvihub.common.constants import API_HOST, WEB_HOST, DEBUG


class SavviHubClient:
    def __init__(self, *, session=requests.Session(), token=None, url=API_HOST, content_type='application/json'):
        self.session = session
        self.url = url
        self.token = token
        
        session.headers = {'content-type': content_type}
        if token:
            session.headers['authorization'] = 'Token %s' % token

    def get(self, url, params=None, raise_error=False, **kwargs):
        r = self.session.get(f'{self.url}{url}', params=params, **kwargs)
        if DEBUG:
            print({
                'method': 'GET',
                'url': url,
                'params': params,
                'status_code': r.status_code if isinstance(r, requests.Response) else None,
                'response': r.text if isinstance(r, requests.Response) else None,
            })
        if raise_error:
            r.raise_for_status()
        return r

    def get_all(self, url, params=None, raise_error=False, **kwargs):
        raw_r = self.get(url, params=params, raise_error=raise_error, **kwargs)
        r = PaginatedMixin(raw_r.json())
        results = []

        fetched_items = 0
        while True:
            fetched_items += len(r.results)
            results.extend(r.results)
            if fetched_items >= r.total:
                break
            raw_r = self.get(url, params={**params, 'after': r.endCursor}, raise_error=raise_error, **kwargs)
            r = PaginatedMixin(raw_r.json())
        return results

    def get_all_without_pagination(self, url, params=None, raise_error=False, **kwargs):
        raw_r = self.get(url, params=params, raise_error=raise_error, **kwargs)
        r = SavviHubListResponse(raw_r.json())
        return r.results

    def post(self, url, data, raise_error=False, **kwargs):
        r = self.session.post(f'{self.url}{url}', json=data, **kwargs)
        if DEBUG:
            print({
                'method': 'POST',
                'url': url,
                'request': data,
                'status_code': r.status_code if isinstance(r, requests.Response) else None,
                'response': r.text if isinstance(r, requests.Response) else None,
            })
        if raise_error:
            r.raise_for_status()
        return r

    def delete(self, url, raise_error=False, **kwargs):
        r = self.session.delete(f'{self.url}{url}', **kwargs)
        if DEBUG:
            print({
                'method': 'DELETE',
                'url': url,
                'status_code': r.status_code if isinstance(r, requests.Response) else None,
                'response': r.text if isinstance(r, requests.Response) else None,
            })
        if raise_error:
            r.raise_for_status()
        return r

    def patch(self, url, data, raise_error=False, **kwargs):
        r = self.session.patch(f'{self.url}{url}', json=data, **kwargs)
        if DEBUG:
            print({
                'method': 'PATCH',
                'url': url,
                'request': data,
                'status_code': r.status_code if isinstance(r, requests.Response) else None,
                'response': r.text if isinstance(r, requests.Response) else None,
            })
        if raise_error:
            r.raise_for_status()
        return r

    def get_my_info(self):
        r = self.get(f'/v1/api/accounts/me/')
        if r.status_code != 200:
            return None
        return SavviHubUser(r.json())

    def check_signin_token(self):
        r = self.post(f'/v1/api/accounts/signin/cli/token/', {})
        r.raise_for_status()
        return r.json()['cli_token']

    def check_signin(self, cli_token):
        r = self.get(f'/v1/api/accounts/signin/cli/check/', {
            'cli_token': cli_token,
        })
        r.raise_for_status()
        return r.json()['signin_success'], r.json()['access_token']

    def volume_create(self, workspace, role_type='experiment-input', **kwargs):
        r = self.post(f'/v1/api/volumes/', {
            'workspace_slug': workspace,
            'role_type': role_type,
        }, **kwargs)
        return SavviHubVolume(r.json())

    def volume_read(self, volume_id, **kwargs):
        r = self.get(f'/v1/api/volumes/{volume_id}/', **kwargs)
        return SavviHubVolume(r.json())

    def volume_file_list(self, volume_id, *, snapshot='latest', prefix='', recursive='false', **kwargs) \
            -> typing.List[SavviHubFileObject]:
        r = self.get(f'/v1/api/volumes/{volume_id}/files/',
                     params={'prefix': prefix, 'recursive': recursive, 'snapshot': snapshot}, **kwargs)
        if r.status_code == 500:
            r.raise_for_status()
        elif r.status_code == 404:
            return []
        return [SavviHubFileObject(x) for x in r.json().get('results')]

    def volume_file_read(self, volume_id, path, snapshot, **kwargs):
        r = self.get(f'/v1/api/volumes/{volume_id}/files/read/', params={'path': path, 'snapshot': snapshot}, **kwargs)
        if r.status_code == 500:
            r.raise_for_status()
        elif r.status_code == 404:
            return None
        return SavviHubFileObject(r.json())

    def volume_file_delete(self, volume_id, path, is_dir):
        r = self.delete(f'/v1/api/volumes/{volume_id}/files/delete/', params={'path': path, 'is_dir': is_dir})
        if r.status_code != 200:
            return None
        return [SavviHubFileMetadata(x) for x in r.json().get('DeletedFiles')]

    def volume_file_create(self, volume_id, path, is_dir, **kwargs):
        return self.post(f'/v1/api/volumes/{volume_id}/files/', {
            'path': path,
            'is_dir': is_dir
        }, **kwargs)

    def volume_file_uploaded(self, volume_id, path, **kwargs):
        return self.post(f'/v1/api/volumes/{volume_id}/files/uploaded/', {
            'path': path,
        }, **kwargs)

    def snapshot_read(self, volume_id, ref, **kwargs):
        r = self.get(f'/v1/api/volumes/{volume_id}/snapshots/{ref}/', **kwargs)
        if r.status_code != 200:
            return None
        return SavviHubSnapshot(r.json())

    def experiment_token_read(self, **kwargs):
        r = self.get(f'/v1/api/experiments/', **kwargs)
        if r.status_code != 200:
            return None
        return SavviHubExperiment(r.json())

    def experiment_read(self, workspace, project, experiment_number, **kwargs) -> SavviHubExperiment:
        return SavviHubExperiment(
            self.get(f'/v1/api/workspaces/{workspace}/projects/{project}/experiments/{experiment_number}',
                     **kwargs).json())

    def experiment_list(self, workspace, project, **kwargs):
        return [SavviHubExperiment(x)
                for x in self.get_all_without_pagination(
                f'/v1/api/workspaces/{workspace}/projects/{project}/experiments/?orderby.direction=DESC', **kwargs)]

    def experiment_log(self, workspace, project, experiment_number, **kwargs):
        return [SavviHubExperimentLog(x)
                for x in self.get(
                f'/v1/api/workspaces/{workspace}/projects/{project}/experiments/{experiment_number}/log/',
                **kwargs).json().get('logs')]

    def experiment_create(self, workspace, project, image_url, resource_spec_id, git_ref, git_diff_file_path,
                          input_volume_id, start_command, dataset_mount_infos, env_vars, **kwargs):
        return self.post(f'/v1/api/workspaces/{workspace}/projects/{project}/experiments/', {
            'image_url': image_url,
            'resource_spec_id': resource_spec_id,
            'git_ref': git_ref,
            'dataset_mount_infos': dataset_mount_infos,
            'git_diff_file_path': git_diff_file_path,
            'input_volume_id': input_volume_id,
            'env_vars': env_vars,
            'start_command': start_command,
        }, **kwargs)

    def experiment_metrics_update(self, experiment_id, metrics: typing.Dict[str, typing.List[SavviHubExperimentMetric]], **kwargs):
        return self.post(f'/v1/api/experiments/{experiment_id}/metrics/', {
            'metrics': metrics,
        }, **kwargs)

    def experiment_system_metrics_update(self, experiment_id, metrics: typing.Dict[str, typing.List[SavviHubExperimentMetric]], **kwargs):
        return self.post(f'/v1/api/experiments/{experiment_id}/system_metrics/', {
            'system_metrics': metrics,
        }, **kwargs)

    def kernel_image_list(self, workspace):
        results = self.get_all_without_pagination(f'/v1/api/workspaces/{workspace}/kernels/images/')
        return [SavviHubKernelImage(x) for x in results]

    def kernel_resource_list(self, workspace):
        results = self.get_all_without_pagination(f'/v1/api/workspaces/{workspace}/kernels/resource_specs')
        return [SavviHubKernelResource(x) for x in results]

    def workspace_list(self, **kwargs):
        r = self.get(f'/v1/api/workspaces/', **kwargs)
        return [SavviHubWorkspace(x) for x in r.json().get('workspaces')]

    def workspace_read(self, workspace):
        r = self.get(f'/v1/api/workspaces/{workspace}/')
        if r.status_code == 404:
            return None
        elif r.status_code != 200:
            r.raise_for_status()
        return SavviHubWorkspace(r.json())

    def project_read(self, workspace, project):
        r = self.get(f'/v1/api/workspaces/{workspace}/projects/{project}/')
        if r.status_code == 404:
            return None
        elif r.status_code != 200:
            r.raise_for_status()
        return SavviHubProject(r.json())

    def project_github_create(self, workspace, project, github_owner, github_repo, **kwargs):
        return SavviHubProject(self.post(f'/v1/api/workspaces/{workspace}/projects_github/', {
            'slug': project,
            'github_owner': github_owner,
            'github_repo': github_repo,
        }, **kwargs).json())

    def public_dataset_list(self, **kwargs):
        results = self.get_all(f'/v1/api/datasets/public/', **kwargs)
        return [SavviHubDataset(x) for x in results]

    def dataset_list(self, workspace, **kwargs):
        results = self.get_all(f'/v1/api/workspaces/{workspace}/datasets/', **kwargs)
        if not results:
            return []
        return [SavviHubDataset(x) for x in results]

    def dataset_read(self, workspace, dataset, **kwargs):
        r = self.get(f'/v1/api/workspaces/{workspace}/datasets/{dataset}/', **kwargs)
        if r.status_code != 200:
            return None
        return SavviHubDataset(r.json())

    def dataset_snapshot_file_list(self, workspace, dataset, ref, **kwargs):
        r = self.get(f'/v1/api/workspaces/{workspace}/datasets/{dataset}/snapshots/{ref}/files/', **kwargs)
        return [SavviHubFileObject(x) for x in r.json().get('results')]

    def dataset_create(self, workspace, slug, is_public, description, **kwargs):
        r = self.post(f'/v1/api/workspaces/{workspace}/datasets/', {
            'slug': slug,
            'is_public': is_public,
            'description': description,
        }, **kwargs)
        if r.status_code == 409:
            typer.echo(f"Duplicate entity \"{workspace}/{slug}\". Try another dataset name!")
            return
        return SavviHubDataset(r.json())

    def dataset_gs_create(self, workspace, slug, is_public, description, gs_path, **kwargs):
        r = self.post(f'/v1/api/workspaces/{workspace}/datasets_gs/', {
            'slug': slug,
            'is_public': is_public,
            'description': description,
            'gs_path': gs_path
        }, **kwargs)
        if r.status_code == 409:
            typer.echo(f"Duplicate entity \"{workspace}/{slug}\". Try another dataset name!")
            return
        return SavviHubDataset(r.json())

    def dataset_s3_create(self, workspace, slug, is_public, description, s3_path, aws_role_arn, **kwargs):
        r = self.post(f'/v1/api/workspaces/{workspace}/datasets_s3/', {
            'slug': slug,
            'is_public': is_public,
            'description': description,
            's3_path': s3_path,
            'aws_role_arn': aws_role_arn,
        }, **kwargs)
        if r.status_code == 409:
            typer.echo(f"Duplicate entity \"{workspace}/{slug}\". Try another dataset name!")
            return
        return SavviHubDataset(r.json())

    @staticmethod
    def get_full_info(workspace, project, experiment, form):
        return \
            f'\n\tFull {form} info at:\n' \
            f'\t\t{WEB_HOST}/{workspace}/{project}/experiments/{experiment}/{form}\n'

    @staticmethod
    def get_full_info_project(workspace, project):
        return \
            f'\n\tFull project info at:\n' \
            f'\t\t{WEB_HOST}/{workspace}/{project}\n'

    @staticmethod
    def get_full_info_dataset(workspace, dataset):
        return \
            f'\n\tFull dataset info at:\n' \
            f'\t\t{WEB_HOST}/{workspace}/datasets/{dataset}\n'

    @staticmethod
    def get_full_info_experiment(workspace, project, experiment):
        return \
            f'\n\tFull experiment info at:\n' \
            f'\t\t{WEB_HOST}/{workspace}/{project}/experiments/{experiment}\n'

    @staticmethod
    def get_download_url(volume_id, path):
        return f'{WEB_HOST}/file-download/{volume_id}/{path}'
