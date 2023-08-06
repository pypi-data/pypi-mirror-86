Feature: Boundaries
  As a DevOps,
  I want to see the boundaries of a system
  so that I know how to interact with it.

  Scenario Outline: Exposed ports
    Given a file named "compose.yml" with:
      """
      version: "2"
      services:
        service:
          volumes:
          - type: bind
            source: ./kvmnt
            target: /kvmnt
      """
    When I run `bash -c "PATH=./bin:$PATH compose_plantuml --boundaries compose.yml"`
    Then it should pass with exactly:
      """
      skinparam componentStyle uml2
      database service_log {
        [/log] as volume_1
      }
      [service] --> volume_1

      """

    Examples: TCP Port
      | port | resulting port |
      | 8080 | 8080           |
