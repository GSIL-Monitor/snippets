require_relative './sshkey.rb'

if ARGF.argv.length < 1 then
  exit
end

f = ARGF.argv.shift

_ = File.read(f)
__ = SSHKey.valid_ssh_public_key? _

p __

if __ then
  p (SSHKey.ssh_public_key_bits _)
  p (SSHKey.fingerprint _)
  p (SSHKey.sha256_fingerprint _)
  key_type, key = SSHKey.parse_ssh_public_key(_)
  p key
  comment = SSHKey.ssh_key_comment(_)
  p "comment: #{comment}"
  p SSHKey::SSH_TYPES.invert[key_type]
end
