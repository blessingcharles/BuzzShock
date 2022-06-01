# https://longliveruby.com/articles/rails-request-cycle
# https://github.com/rack/rack/blob/master/SPEC.rdoc
class ImitationOfRails
    def call(env)
        # puts(env)
        # env.each { |key, value| puts "k: #{key}, v: #{value}" }
        buf = env["rack.input"].read
        [200, {'Content-Type' => 'text/plain'}, ['Body length: ' + buf.length.to_s + ' Body: ' + buf]]
    end
end
