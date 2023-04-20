{{/*
Expand the name of the chart.
*/}}
{{- define "decision.name" -}}
{{- .Values.decisionService.nameOverride | default "decision" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "decision.labels" -}}
helm.sh/chart: {{ include "global.chart" . }}
{{ include "decision.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "decision.selectorLabels" -}}
app.kubernetes.io/name: {{ include "decision.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "decision.serviceAccountName" -}}
{{- if .Values.decisionService.serviceAccount.create }}
{{- .Values.decisionService.serviceAccount.name | default (include "decision.name" .) }}-serviceaccount
{{- else }}
{{- .Values.decisionService.serviceAccount.name | default "default" }}
{{- end }}
{{- end }}

{{- define "decision.serviceName" -}}
{{- include "decision.name" . }}-svc
{{- end }}

{{- define "decision.servicePort" -}}
{{- .Values.decisionService.servicePort | default 80 -}}
{{- end }}
