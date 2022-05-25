package io.clouditor.graph.testing

import com.fasterxml.jackson.databind.ObjectMapper
import com.fasterxml.jackson.dataformat.yaml.YAMLFactory
import com.fasterxml.jackson.module.kotlin.KotlinModule
import de.fraunhofer.aisec.cpg.TranslationResult
import de.fraunhofer.aisec.cpg.passes.Pass
import io.clouditor.graph.*
import io.clouditor.graph.passes.golang.appendPath
import java.nio.file.Files

class LocalTestingPass : Pass() {

    override fun accept(t: TranslationResult) {
        val applications = listOf(App.rootPath)

        for (rootPath in applications) {
            // val workflowPath = rootPath.resolve("ppg-testing-library").resolve("config")
            // here, the config.yml will be analyzed, assuming that in the test case, we have
            // specified the exact test case location, e.g.
            // "/Users/kunz/cloud-property-graph/ppg-testing-library/Non-Repudiation/NR1-credentials-non-repudiation/Go/zerolog"
            rootPath.toFile().walkTopDown().iterator().forEach { file ->
                if (file.extension == "yml") {
                    val mapper = ObjectMapper(YAMLFactory())
                    mapper.registerModule(KotlinModule())

                    Files.newBufferedReader(file.toPath()).use {
                        val config = mapper.readValue(it, TestConfig::class.java)
                        handleConf(config, t)
                    }
                }
            }
        }
    }

    private fun handleConf(conf: TestConfig, t: TranslationResult) {
        val controllers =
            t.additionalNodes.filter { it is HttpRequestHandler }.map { it as HttpRequestHandler }

        for (service in conf.services) {
            if (service.type == "server") {
                for (controller in controllers) {
                    for (endpoint in controller.httpEndpoints) {
                        var url = service.host?.appendPath(controller.path)
                        url = url?.appendPath(endpoint.path)

                        val proxy =
                            ProxiedEndpoint(
                                listOf(endpoint),
                                NoAuthentication(),
                                endpoint.handler,
                                endpoint.method,
                                endpoint.path,
                                null,
                                url
                            )
                        proxy.addNextDFG(endpoint)
                        t += proxy
                    }
                }

                val application =
                    Application(
                        mutableListOf(),
                        // TODO how to get the programming language?
                        "",
                        mutableListOf(),
                        t.translationUnits,
                    )
                application.name = service.type
                t += application
            }
        }

        for (service in conf.services) {
            if (service.name == "postgres") {
                val db =
                    RelationalDatabaseService(
                        mutableListOf<DatabaseStorage>(),
                        null,
                        null,
                        null,
                        null,
                        mapOf()
                    )
                db.name = service.name
                t += db
            }
            if (service.name == "mongo") {
                val db =
                    DocumentDatabaseService(
                        mutableListOf<DatabaseStorage>(),
                        null,
                        null,
                        null,
                        null,
                        mapOf()
                    )
                db.name = service.name
                t += db
            }
        }
    }

    override fun cleanup() {}
}
